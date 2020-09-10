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
    <link rel="stylesheet" type="text/css" href="{% static 'restaurant/css/magic-input.css' %}">
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
                <div class="left__menu__lists">
                    <ul>
                        <li>
                            <a href="{% url 'dashboard:restaurant-list' %}"><i class="fa fa-cutlery" aria-hidden="true"></i> Restaurant List</a>
                        </li>
                        <li>
                            <a href="{% url 'dashboard:category-list' %}"><i class="fa fa-cutlery" aria-hidden="true"></i> Category List</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-users" aria-hidden="true"></i> User List</a>
                        </li>
                        <li>
                            <a href="{% url 'dashboard:request-list' %}"><i class="fa fa-inbox" aria-hidden="true"></i> Restaurant Requests</a>
                        </li>
                        {% if request.user.is_superuser %}
                        <li>
                            <a href="{% url 'dashboard:support-staffs' %}"><i class="fa fa-user-secret" aria-hidden="true"></i> Staffs</a>
                        </li>
                        {% endif %}
                        <li>
                            <a href="{% url 'dashboard:delivery-person-list' %}"><i class="fa fa-truck" aria-hidden="true"></i> Delivery Person</a>
                        </li>
                        <li>
                            <a href="{% url 'dashboard:change-password' %}"><i class="fa fa-wrench" aria-hidden="true"></i> Change Password</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-money" aria-hidden="true"></i> My Earnings</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="col-md-9 ml-auto">
            <div class="row">
                <div class="right__body__sec">
                    <div class="pd-tb-md">
                        <div class="rb-pd-rl rs-in-hl">
                            <div class="rs-in">
                                <div class="rs-in-tx">
                                    <div class="rs-nm">
                                        {{ request.user.username|title }}
                                    </div>
                                    <div class="rs-ad">
                                        {{ request.user.first_name }} {{ request.user.last_name }}
                                    </div>
                                </div>
                            </div>
                            <div class="ac-bt-hl">
                                <a class="ac-bt" href="{% url 'logout' %}">Logout</a>
                            </div>
                        </div>
                    </div>
