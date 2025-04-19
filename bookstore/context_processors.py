
def permission_context(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user
    return {
        "can_view_books": user.has_perm('bookstore.view_book'),
        "can_view_orders": user.has_perm('bookstore.view_order'),
        "can_view_categories": user.has_perm('bookstore.view_category'),
        "can_view_stockin": user.has_perm('bookstore.view_stockin'),
        "can_view_stockout": user.has_perm('bookstore.view_stockout'),
        "can_view_report": user.has_perm('bookstore.view_report'),
        "can_view_users": user.has_perm('auth.view_user'),
    }