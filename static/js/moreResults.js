// Track the current page of results
var currentPage = 2;  // Start from the second page since the first page is already loaded
var loading = false;  // Flag to prevent multiple simultaneous requests

// Function to load more results when scrolling down
function loadMoreResults() {
    // Check if a request is already in progress
    if (loading) {
        return;
    }

    loading = true;

    // Get the current search query from the URL
    var searchQuery = getSearchQueryFromUrl();

    // Fetch more results from the server using AJAX with jQuery
    $.get('/search', { search_query: searchQuery, page: currentPage })
        .done(function (response) {
            // Append the new results to the existing container
            var container = $('#thumbnail-container');
            container.append(response['html']);

            // Increment the current page
            currentPage += 1;
        })
        .fail(function (error) {
            console.error('Error handling AJAX response:', error);
        })
        .always(function () {
            // Reset the loading flag regardless of success or failure
            loading = false;
        });
}

// Function to get the search query from the URL
function getSearchQueryFromUrl() {
    var urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('search_query') || '';
}

// Add an event listener for scrolling
$(window).scroll(function () {
    // Check if the user has scrolled to the bottom of the page
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
        loadMoreResults();
    }
});
