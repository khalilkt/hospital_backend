
def get_queryset_by_date(queryset, year = None, month = None, day = None):
    if not day and not month and not year:
        return queryset
    if year:
        queryset = queryset.filter(created_at__year = year)
    if month:
        queryset = queryset.filter(created_at__month = month)
    if day:
        queryset = queryset.filter(created_at__day = day)
    return queryset