let
    Source = Csv.Document(File.Contents(DataFolder & "\restaurants.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, {
        {"RestaurantID", Text.Trim, type text}, {"RestaurantName", Text.Trim, type text},
        {"City", Text.Trim, type text}, {"Area", Text.Trim, type text},
        {"PrimaryCuisine", Text.Trim, type text}, {"CostBucket", Text.Trim, type text},
        {"OnlineDelivery", Text.Trim, type text}, {"TableBooking", Text.Trim, type text}
    }),
    ChangedTypes = Table.TransformColumnTypes(TrimmedText, {
        {"CostForTwo", Currency.Type}, {"Rating", type number}, {"Votes", Int64.Type}
    }),
    NormalizedOnline = Table.TransformColumns(ChangedTypes, {{"OnlineDelivery", Text.Proper, type text}}),
    NormalizedBooking = Table.TransformColumns(NormalizedOnline, {{"TableBooking", Text.Proper, type text}}),
    ReplacedRatingErrors = Table.ReplaceErrorValues(NormalizedBooking, {{"Rating", null}}),
    ReplacedVoteErrors = Table.ReplaceErrorValues(ReplacedRatingErrors, {{"Votes", 0}}),
    AddedRatingBand = Table.AddColumn(ReplacedVoteErrors, "RatingBand", each
        if [Rating] = null then "Unrated"
        else if [Rating] >= 4.2 then "Excellent"
        else if [Rating] >= 3.7 then "Good"
        else if [Rating] >= 3.0 then "Average"
        else "Needs Improvement", type text)
in
    AddedRatingBand
