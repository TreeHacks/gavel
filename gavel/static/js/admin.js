$(function() {
    $(".category-btn").click(function() {
        var selectedCategory = $(this).text();
        if ($(this).hasClass("selected")) {
            // go to all.
            $(this).removeClass("selected");
            $(".category-btn .category-btn-all").click();
        }
        $(".category-btn").removeClass("selected");
        $(this).addClass("selected");
        $("table#items tr").each(function() {
            var categories = $(this).attr("data-categories");
            if (!categories) {
                return;
            }
            categories = categories.split(",").map(e => $.trim(e));
            if (selectedCategory === "All" || categories.indexOf(selectedCategory) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    })
});