let
    Source = Csv.Document(File.Contents(DataFolder & "\customers.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, {
        {"CustomerID", Text.Trim, type text}, {"HomeCity", Text.Trim, type text},
        {"AgeBand", Text.Trim, type text}, {"PreferredChannel", Text.Trim, type text},
        {"CustomerSegment", Text.Trim, type text}
    }),
    ChangedTypes = Table.TransformColumnTypes(TrimmedText, {
        {"SignupDate", type date}, {"LifetimeRevenue", Currency.Type}, {"LifetimeOrders", Int64.Type}
    }),
    ReplacedNullSegment = Table.ReplaceValue(ChangedTypes, null, "Unknown", Replacer.ReplaceValue, {"CustomerSegment"}),
    NormalizedSegment = Table.TransformColumns(ReplacedNullSegment, {{"CustomerSegment", Text.Proper, type text}})
in
    NormalizedSegment
