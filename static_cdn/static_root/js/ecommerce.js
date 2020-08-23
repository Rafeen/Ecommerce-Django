$(document).ready(function(){
    // Contact Form Handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndPoint = contactForm.attr("action")
    function displaySubmitting(submitBtn, doSubmit) {
        if (doSubmit){
            submitBtn.addClass("disabled");
            submitBtn.html("<i class='fa fa-spinner fa-spin'></i> Sending...");
        }else {
            submitBtn.removeClass("disabled");
            submitBtn.html("<i class='fa fa-paper-plane-o' aria-hidden='true'></i> Send");
        }
    }
    contactForm.submit(function (event) {
        var contactFormSubmithBtn = contactForm.find("[type='submit']");
        event.preventDefault()
        var contactFormData = contactForm.serialize()
        thisForm = $(this)
        displaySubmitting(contactFormSubmithBtn, true)

        $.ajax({
            url: contactFormEndPoint,
            method: contactFormMethod,
            data: contactFormData,
            success: function (data) {
                contactForm[0].reset()
                $.alert({
                    title:"Success",
                    content: data.message,
                    theme: "modern",
                })
                setTimeout(function () {
                    displaySubmitting(contactFormSubmithBtn, false)
                }, 2000)
            },
            error: function (errorData) {
                console.log(errorData)
                console.log(errorData.responseJSON)
                var jsonData = errorData.responseJSON
                var message = ""
                $.each(jsonData, function (key, value) {
                    message += key + ":" + value[0].message + "</br>"
                })
                $.alert({
                    title: "Oops",
                    content: message,
                    theme: "modern",
                })
                setTimeout(function () {
                    displaySubmitting(contactFormSubmithBtn, false)
                }, 500)
            }
        })
    })

    // auto search
    var searchForm = $(".search-form");
    var searchInput = searchForm.find("[name='q']");
    var searchBtn = searchForm.find("[type='submit']");
    var typingTimer;
    var typingInterval = 700;

    searchInput.keyup(function (event) {
        // key up
        clearTimeout(typingTimer);
        typingTimer = setTimeout(performSearch, typingInterval)
    });
    searchInput.keydown(function (event) {
        // key down
        clearTimeout(typingTimer);
    });
    function displaySearching() {
        searchBtn.addClass("disabled");
        searchBtn.html("<i class='fa fa-spinner fa-spin'></i> Searching...");
    }
    function performSearch() {
        displaySearching()
        var query = searchInput.val();
        setTimeout(function () {
            window.location.href = '/search/?q=' + query

        },1000)
    }

    // cart and add product
    var productForm = $(".form-product-ajax") // #form-product-ajax

    productForm.submit(function(event){
        event.preventDefault();
        // console.log("Form is not sending")
        var thisForm = $(this)
        // var actionEndpoint = thisForm.attr("action"); // API Endpoint
        var actionEndpoint = thisForm.attr("data-endpoint")
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                var submitSpan = thisForm.find(".submit-span")
                if (data.added){
                    submitSpan.html("In cart <button type='submit' class='btn btn-danger'>Remove?</button>")
                } else {
                    submitSpan.html("<button type='submit'  class='btn btn-success'>Add to cart</button>")
                }
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.count)
                var currentPath = window.location.href

                if (currentPath.indexOf("cart") != -1) {
                    refreshCart()
                }
            },
            error: function(errorData){
                console.log("error")
                console.log(errorData)
            }
        })
    });
    function refreshCart() {
        console.log("in current cart");
        var cartTable = $(".cart-table");
        var cartBody = cartTable.find(".cart-body");
        var refreshCartUrl = "{% url 'cart:cart-api' %}";
        var refreshMethod = "GET";
        var data = {};
        var productRows = cartBody.find('.cart-product');
        var currentUrl = window.location.href;

        $.ajax({
            url: refreshCartUrl,
            method: refreshMethod,
            data: data,
            success: function(data){
                console.log("success refresh cart");
                console.log(data);
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form");
                if (data.products.length >0){
                    productRows.html(" ");
                    i = data.products.length;
                    $.each(data.products, function(index, value){
                        console.log(value);
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone();
                        newCartItemRemove.css("display", "block");
                        console.log("button un hidden");
                        console.log(value.id);
                        newCartItemRemove.find(".cart-item-product-id").val(value.id);
                        cartBody.prepend("<tr><th scope=\"row\">" +i+ "</th><td><a href='" +value.url+ "'>" +value.title+ "</a>" +newCartItemRemove.html()+ "</td><th>" +value.price+ "</th></tr>");
                        i--
                    });
                    cartBody.find(".cart-total").text(data.total);
                    cartBody.find(".cart-subtotal").text(data.subtotal);
                }else{
                    console.log("cart empty refreshing page");
                    window.location.href = currentUrl;
                }
            },
            error: function(errorData){
                console.log("error refresh cart");
                console.log(errorData);
            }
        })
    }
})