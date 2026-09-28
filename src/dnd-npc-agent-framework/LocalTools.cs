using System.ComponentModel;
using System.Diagnostics;

namespace DnDNpcAgent;

internal class LocalTools
{
	public const string ActivitySourceName = "dnd-npc-agent-framework-local-tools";

	public required ActivitySource ActivitySource { private get; init; }

	#region DEMO1LOCAL_TOOL
	/// <summary>
	/// Throws a die with the specified number of sides and an optional modifier, returning the result.
	/// </summary>
	/// <param name="sides">Number of sides on the die.</param>
	/// <param name="modifier">Optional modifier to be applied to the roll.</param>
	/// <returns>The final result of the die roll, including any modifier.</returns>
	[Description("Throws a die with the specified number of sides and an optional modifier, returning the result.")]
	public int ThrowDie(
		[Description("Number of sides on the die.")] uint sides = 20,
		[Description("Optional modifier to be applied to the roll.")] int modifier = default)
	{
		using var activity = ActivitySource.StartActivity("ThrowDie");
		ArgumentOutOfRangeException.ThrowIfEqual<uint>(sides, 0);
	
		var random = new Random();
		int result = random.Next(1, (int)sides + 1);

		string diceNotation = modifier is not default(int) ? $"d{sides} + {modifier}" : $"d{sides}";
		int finalResult = result + modifier;

		activity?.SetTag("dice.notation", diceNotation);
		activity?.SetTag("dice.result", finalResult);
		activity?.SetTag("dice.sides", sides);

		return finalResult;
	}
	#endregion
}