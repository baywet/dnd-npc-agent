// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
using Azure.AI.Extensions.OpenAI;
using Azure.AI.Projects;
using Azure.Identity;
using DotNetEnv;
using OpenAI.Files;
using OpenAI.FineTuning;
using Azure.ResourceManager;
using Azure.ResourceManager.CognitiveServices;
using Azure.ResourceManager.CognitiveServices.Models;
using System.ClientModel;
using System.ClientModel.Primitives;
using System.Runtime.CompilerServices;

#pragma warning disable OPENAI001

// Load environment variables from .env file
Env.TraversePath().Load();

string trainingFilePath = Path.Combine(AppContext.BaseDirectory, "data", "dnd_npc_data_train.jsonl");
string validationFilePath = Path.Combine(AppContext.BaseDirectory, "data", "dnd_npc_data_valid.jsonl");
string subscriptionID = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID") ?? throw new InvalidOperationException("AZURE_SUBSCRIPTION_ID environment variable is not set.");
string resourceGroup = Environment.GetEnvironmentVariable("AZURE_RESOURCE_GROUP") ?? throw new InvalidOperationException("AZURE_RESOURCE_GROUP environment variable is not set.");
string foundryName = Environment.GetEnvironmentVariable("AZURE_AI_ACCOUNT_NAME") ?? throw new InvalidOperationException("AZURE_AI_ACCOUNT_NAME environment variable is not set.");

// Initialize the clients
var endpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT") ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT environment variable is not set.");
var modelDeploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? throw new InvalidOperationException("AZURE_AI_MODEL_DEPLOYMENT_NAME environment variable is not set.");
var completedJob = Environment.GetEnvironmentVariable("COMPLETED_JOB");
DefaultAzureCredential credential = new();

AIProjectClient projectClient = new(new Uri(endpoint), credential);
ProjectFilesClient fileClient = projectClient.ProjectOpenAIClient.GetProjectFilesClient();
FineTuningClient fineTuningClient = projectClient.ProjectOpenAIClient.GetFineTuningClient();
FineTuningJob fineTuningJob;
if (string.IsNullOrEmpty(completedJob))
{
    // Upload training and validation files.
    // Training file
    Console.WriteLine("Uploading training file...");
    OpenAIFile trainFile = await UploadFile(fileClient, trainingFilePath);
    Console.WriteLine($"Uploaded training file with ID: {trainFile.Id}");
    // Validation file
    Console.WriteLine("Uploading validation file...");
    OpenAIFile validFile = await UploadFile(fileClient, validationFilePath);
    Console.WriteLine($"Uploaded validation file with ID: {validFile.Id}");

    // Create supervised fine-tuning job
    Console.WriteLine("Creating Direct Preference Optimization fine-tuning job...");

    // Azure requires training_type: "global" — there is no strongly-typed property
    // for this on FineTuningOptions, so we send the request via BinaryContent and
    // hydrate FineTuningJob from the response.
    var requestBody = BinaryData.FromObjectAsJson(new
    {
        model = modelDeploymentName,
        training_file = trainFile.Id,
        validation_file = validFile.Id,
        trainingType = "GlobalStandard",
        method = new
        {
            type = "dpo",
            dpo = new
            {
                hyperparameters = new
                {
                    n_epochs = 1,
                    batch_size = 4,
                    learning_rate_multiplier = 0.0001
                }
            }
        }
    });

    using BinaryContent requestContent = BinaryContent.Create(requestBody);
    fineTuningJob = await fineTuningClient.FineTuneAsync(
        requestContent,
        waitUntilCompleted: false,
        options: null);
    Console.WriteLine($"Created fine-tuning job: {fineTuningJob.JobId}");

    // Wait for fine tuning task to complete. It may take a while!
    while (fineTuningJob.Status != FineTuningStatus.Succeeded && fineTuningJob.Status != FineTuningStatus.Failed || fineTuningJob.Status != FineTuningStatus.Cancelled)
    {
        await Task.Delay(TimeSpan.FromMinutes(10));
        fineTuningJob = await fineTuningClient.GetJobAsync(fineTuningJob.JobId);
    }
}
else
{
    fineTuningJob = await fineTuningClient.GetJobAsync(completedJob);
}
if (fineTuningJob.Status != FineTuningStatus.Succeeded)
{
    throw new InvalidOperationException($"The fine training job {fineTuningJob.JobId} has failed.");
}
Console.WriteLine($"The fine training job {fineTuningJob.JobId} completed successfully.");
// List checkpoints (job needs to be in terminal state)
Console.WriteLine($"Listing checkpoints of fine-tuning job: {fineTuningJob.JobId}");
await foreach (FineTuningCheckpoint checkpoint in fineTuningJob.GetCheckpointsAsync(new GetCheckpointsOptions()))
{
    Console.WriteLine($"Checkpoint: {checkpoint.Id} at step {checkpoint.StepNumber}");
}

// After the fine tuning job has completed, we can deploy the fine tuned model.
// It requires a completed fine-tuning job and takes approximately 30 minutes to complete.
string deploymentName = $"ft-deployment-{fineTuningJob.BaseModel}-{DateTimeOffset.UtcNow:yyyy-MM-dd}";
var armClient = new ArmClient(credential);
// Get Cognitive Services account
var resourceId = CognitiveServicesAccountResource.CreateResourceIdentifier(
    subscriptionID,
    resourceGroup,
    foundryName);
var accountResource = armClient.GetCognitiveServicesAccountResource(resourceId);

// Deploy the model
var deploymentData = new CognitiveServicesAccountDeploymentData
{
    Properties = new CognitiveServicesAccountDeploymentProperties
    {
        Model = new CognitiveServicesAccountDeploymentModel
        {
            Format = "OpenAI",
            Name = fineTuningJob.Value,
            Version = "1"
        }
    },
    Sku = new CognitiveServicesSku("GlobalStandard") { Capacity = 50 }
};

await accountResource.GetCognitiveServicesAccountDeployments()
    .CreateOrUpdateAsync(Azure.WaitUntil.Completed, deploymentName, deploymentData);
Console.WriteLine("Model deployment has completed!");

#region Helpers
// Upload file
async static Task<OpenAIFile> UploadFile(ProjectFilesClient fileClient, string path)
{
    using FileStream trainStream = System.IO.File.OpenRead(path);
    OpenAIFile file = await fileClient.UploadFileAsync(
                trainStream,
                Path.GetFileName(path),
                FileUploadPurpose.FineTune);
    while (file.Status != FileStatus.Processed && file.Status != FileStatus.Error)
    {
        await Task.Delay(2);
        file = await fileClient.GetFileAsync(file.Id);
    }
    if (file.Status == FileStatus.Error)
    {
        throw new InvalidOperationException(
            $"File {file.Id} processing failed: {file.StatusDetails}");
    }
    return file;
}
#endregion