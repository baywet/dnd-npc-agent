// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
using Azure.AI.Extensions.OpenAI;
using Azure.AI.Projects;
using Azure.Identity;
using OpenAI.Files;
using OpenAI.FineTuning;
using Azure.ResourceManager;
using Azure.ResourceManager.CognitiveServices;
using Azure.ResourceManager.CognitiveServices.Models;
using System.Runtime.CompilerServices;

#pragma warning disable OPENAI001

string trainingFilePath = Environment.GetEnvironmentVariable("TRAINING_FILE_PATH") ?? "data/dnd_npc_data_train.jsonl";
string validationFilePath = Environment.GetEnvironmentVariable("VALIDATION_FILE_PATH") ?? "data/dnd_npc_data_valid.jsonl";
string subscriptionID = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
string resourceGroup = Environment.GetEnvironmentVariable("RESOURCE_GROUP");
string foundryName = Environment.GetEnvironmentVariable("MICROSOFT_FOUNDRY_NAME");

// Initialize the clients
var endpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = Environment.GetEnvironmentVariable("FOUNDRY_MODEL_NAME");
var completedJob = Environment.GetEnvironmentVariable("COMPLETED_JOB");
DefaultAzureCredential credential = new();

AIProjectClient projectClient = new (new Uri(endpoint), credential);
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
    fineTuningJob = await fineTuningClient.FineTuneAsync(
        modelDeploymentName,
        trainFile.Id,
        waitUntilCompleted: false,
        new()
        {
            TrainingMethod = FineTuningTrainingMethod.CreateDirectPreferenceOptimization(
                epochCount: 1,
                batchSize: 4,
                learningRate: 0.0001),
            ValidationFile = validFile.Id
        });
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
    if (path.StartsWith("data"))
    {
        path = GetFile(Path.Combine([path]));
    }
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

// Get the file, which can be located at source codes.
static string GetFile(string fileName, [CallerFilePath] string pth = "")
{
    var dirName = Path.GetDirectoryName(pth) ?? "";
    return Path.Combine([dirName, fileName]);
}
#endregion