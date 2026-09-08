let
    Source = Csv.Document(File.Contents(DataFolder & "\orders.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, {
        {"OrderID", Text.Trim, type text}, {"CustomerID", Text.Trim, type text},
        {"RestaurantID", Text.Trim, type text}, {"City", Text.Trim, type text},
        {"Area", Text.Trim, type text}, {"PrimaryCuisine", Text.Trim, type text},
        {"CostBucket", Text.Trim, type text}, {"OrderStatus", Text.Trim, type text},
        {"PaymentMethod", Text.Trim, type text}, {"OrderChannel", Text.Trim, type text}
    }),
    ChangedTypes = Table.TransformColumnTypes(TrimmedText, {
        {"OrderDateTime", type datetime}, {"OrderDate", type date}, {"OrderHour", Int64.Type},
        {"OrderAmount", Currency.Type}, {"DeliveryMinutes", type number}, {"IsLate", Int64.Type},
        {"DeliveryDistanceKM", type number}, {"CustomerRating", Int64.Type}
    }),
    ReplacedDeliveryErrors = Table.ReplaceErrorValues(ChangedTypes, {{"DeliveryMinutes", null}}),
    NormalizedStatus = Table.TransformColumns(ReplacedDeliveryErrors, {{"OrderStatus", Text.Proper, type text}}),
    AddedYear = Table.AddColumn(NormalizedStatus, "OrderYear", each Date.Year([OrderDate]), Int64.Type),
    AddedMonth = Table.AddColumn(AddedYear, "OrderMonth", each Date.MonthName([OrderDate]), type text),
    AddedDayPart = Table.AddColumn(AddedMonth, "OrderDaypart", each
        if [OrderHour] < 6 then "Night"
        else if [OrderHour] < 12 then "Morning"
        else if [OrderHour] < 17 then "Afternoon"
        else if [OrderHour] < 22 then "Evening"
        else "Night", type text),
    AddedDeliveryPerformance = Table.AddColumn(AddedDayPart, "DeliveryPerformance", each
        if [OrderStatus] = "Cancelled" then "Cancelled"
        else if [IsLate] = 1 then "Late"
        else "On Time", type text)
in
    AddedDeliveryPerformance
