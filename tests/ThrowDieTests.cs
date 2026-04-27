using System.Text.RegularExpressions;

namespace local_tools.tests;

public class ThrowDieTests
{
    [Fact]
    public void ThrowDie_WithDefaultSides_ReturnsResultBetween1And20()
    {
        for (int i = 0; i < 100; i++)
        {
            var result = ThrowDie();
            Assert.Contains("d20", result);
            Assert.Contains("🎲", result);
            Assert.Matches(@"\*\*(\d+)\*\*", result);

            var numberMatch = Regex.Match(result, @"\*\*(\d+)\*\*");
            int rollResult = int.Parse(numberMatch.Groups[1].Value);
            Assert.InRange(rollResult, 1, 20);
        }
    }

    [Fact]
    public void ThrowDie_WithCustomSides_ReturnsResultWithinRange()
    {
        for (int i = 0; i < 100; i++)
        {
            var result = ThrowDie(6);
            Assert.Contains("d6", result);
            Assert.Contains("🎲", result);

            var numberMatch = Regex.Match(result, @"\*\*(\d+)\*\*");
            int rollResult = int.Parse(numberMatch.Groups[1].Value);
            Assert.InRange(rollResult, 1, 6);
        }
    }

    [Fact]
    public void ThrowDie_WithSingleSidedDie_AlwaysReturnsOne()
    {
        var result = ThrowDie(1);
        Assert.Contains("d1", result);
        Assert.Contains("**1**", result);
    }

    [Theory]
    [InlineData(4)]
    [InlineData(8)]
    [InlineData(12)]
    [InlineData(20)]
    [InlineData(100)]
    public void ThrowDie_WithVariousSides_ReturnsValidResult(int sides)
    {
        var result = ThrowDie(sides);
        Assert.Contains($"d{sides}", result);

        var numberMatch = Regex.Match(result, @"\*\*(\d+)\*\*");
        int rollResult = int.Parse(numberMatch.Groups[1].Value);
        Assert.InRange(rollResult, 1, sides);
    }

    [Fact]
    public void ThrowDie_WithZeroSides_ReturnsError()
    {
        var result = ThrowDie(0);
        Assert.Equal("Error: Die must have at least 1 side.", result);
    }

    [Fact]
    public void ThrowDie_WithNegativeSides_ReturnsError()
    {
        var result = ThrowDie(-5);
        Assert.Equal("Error: Die must have at least 1 side.", result);
    }

    [Fact]
    public void ThrowDie_Formatting_IncludesEmoji()
    {
        var result = ThrowDie(20);
        Assert.StartsWith("🎲", result);
    }

    [Fact]
    public void ThrowDie_Formatting_HasProperStructure()
    {
        var result = ThrowDie(20);
        Assert.Matches(@"🎲 Rolled a d\d+: \*\*\d+\*\*", result);
    }

    private static string ThrowDie(int sides = 20)
    {
        if (sides <= 0)
            return "Error: Die must have at least 1 side.";

        var random = new Random();
        int result = random.Next(1, sides + 1);

        return $"🎲 Rolled a d{sides}: **{result}**";
    }
}
