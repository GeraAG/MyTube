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
            //normalViewCount()
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
/*
function normalViewCount() {
    document.querySelectorAll(".view-count").forEach((e) => {
        let n = intToString(Number(e.innerHTML));
        e.innerHTML = n;
        e.classList.remove("view-count");
        e.classList.add("view-count-short");
    });
}

const intToString = num => {
    num = num.toString().replace(/[^0-9.]/g, '');
    if (num < 1000) {
        return num;
    }
    let si = [
      {v: 1E3, s: "K"},
      {v: 1E6, s: "M"},
      {v: 1E9, s: "B"}
      ];
    let index;
    for (index = si.length - 1; index > 0; index--) {
        if (num >= si[index].v) {
            break;
        }
    }
    return (num / si[index].v).toFixed(2).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, "$1") + si[index].s;
};

document.addEventListener("DOMContentLoaded", function() {
    normalViewCount();
  });
*/

// Add an event listener for scrolling
$(window).scroll(function () {
    // Check if the user has scrolled to the bottom of the page
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
        loadMoreResults();
    }
});

window.onload = function() {
    var body = $('#thumbnail-container').outerHeight();
    var win = $(window).height();
    if (body < win ) {
        loadMoreResults();
    }
};
