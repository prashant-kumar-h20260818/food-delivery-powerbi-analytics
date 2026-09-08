let
    StartDate = #date(2023, 1, 1),
    EndDate = #date(2025, 12, 31),
    DateList = List.Dates(StartDate, Duration.Days(EndDate - StartDate) + 1, #duration(1,0,0,0)),
    ToTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    ChangedType = Table.TransformColumnTypes(ToTable, {{"Date", type date}}),
    AddedYear = Table.AddColumn(ChangedType, "Year", each Date.Year([Date]), Int64.Type),
    AddedQuarter = Table.AddColumn(AddedYear, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddedMonthNumber = Table.AddColumn(AddedQuarter, "MonthNumber", each Date.Month([Date]), Int64.Type),
    AddedMonth = Table.AddColumn(AddedMonthNumber, "Month", each Date.MonthName([Date]), type text),
    AddedYearMonth = Table.AddColumn(AddedMonth, "YearMonth", each Date.ToText([Date], "yyyy-MM"), type text),
    AddedDay = Table.AddColumn(AddedYearMonth, "Day", each Date.Day([Date]), Int64.Type),
    AddedDayName = Table.AddColumn(AddedDay, "DayName", each Date.DayOfWeekName([Date]), type text),
    AddedWeek = Table.AddColumn(AddedDayName, "WeekOfYear", each Date.WeekOfYear([Date]), Int64.Type)
in
    AddedWeek
