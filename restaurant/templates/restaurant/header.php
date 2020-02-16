{% load static %}
<!doctype html>
<html lang="en">
<head>
    <!-- Meta Tags -->
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/bootstrap.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/style.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/common.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/responsive.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/jquery.dataTables.min.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/owl.carousel.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/owl.theme.default.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/select2.css' %}">
    <!-- <link rel="stylesheet" type="text/css" href="css/font-awesome.css"> -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
   integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
   crossorigin=""/>
  </head>

  <body>
    <section class="whole__body__wrapper">
    <section class="inner__body__wrapper">
        <div class="col-md-3 for__sidemenu__bg">
            <div class="dash__left__sitemenu">
                <div class="site_logo__holder">
                    <img src="{% static 'restaurant/images/logo.png' %}" alt="">
                </div>
                {% if request.restaurant.id %}
                <div class="left__menu__lists">
                    <ul>
                        <li>
                            <a href="{% url 'restaurant:restaurant-detail' request.restaurant.id %}"><i class="fa fa-tachometer" aria-hidden="true"></i> Restaurant Detail</a>
                        </li>
                        <li>
                            <a href="{% url 'restaurant:category-list' request.restaurant.id %}"><i class="fa fa-cubes" aria-hidden="true"></i> Restaurant Categories</a>
                        </li>
                        <li>
                            <a href="{% url 'restaurant:menu-list' request.restaurant.id %}"><i class="fa fa-cutlery" aria-hidden="true"></i> Menu</a>
                        </li>
                        <li>
                            <a href="{% url 'restaurant:dashboard' request.restaurant.id %}"><i class="fa fa-cutlery" aria-hidden="true"></i> Add Food Item</a>
                        </li>
                        <li>
                            <a href="{% url 'restaurant:order' request.restaurant.id %}"><i class="fa fa-paper-plane-o" aria-hidden="true"></i> Orders</a>
                        </li>
                        <li>
                            <a href="{% url 'restaurant:accepted-order' request.restaurant.id %}"><i class="fa fa-file" aria-hidden="true"></i> Accepted Orders</a>
                        </li>
                        <li>
                            <a href="{% url 'restaurant:change-password' %}"><i class="fa fa-wrench" aria-hidden="true"></i> Change Password</a>
                        </li>
                    </ul>
                </div>
                {% endif %}
            </div>
        </div>
        <div class="col-md-9 ml-auto">
            <div class="row">
                <div class="right__body__sec">
                    <div class="pd-tb-md">
                        {% if request.restaurant %}
                        <div class="rb-pd-rl rs-in-hl">
                            <div class="rs-in">
                                <div class="rs-lg">
                                    {% if request.restaurant.logo %}
                                    <img src="{{ request.restaurant.logo.url }}" alt="">
                                    {% else %}
                                    <img src="{% static 'restaurant/images/rest_logo.jpg' %}" alt="">
                                    {% endif %}
                                </div>
                                <div class="rs-in-tx">
                                    <div class="rs-nm">
                                        {{ request.restaurant.name }}
                                    </div>
                                    <div class="rs-ad">
                                        {{ request.restaurant.location_text }}
                                    </div>
                                </div>
                            </div>
                            <div class="ac-bt-hl">
                                <!-- <a class="ac-bt" href="{% url 'restaurant:restaurant-detail' request.restaurant.id %}">Edit</a> -->
                                <a class="ac-bt" href="{% url 'logout' %}">Logout</a>
                            </div>
                        </div>
                        {% endif %}
                    </div>
