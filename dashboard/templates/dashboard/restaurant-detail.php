{% include 'dashboard/header.php' %}
{% load static %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>{{ restaurant.name|title }}</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <div class="order-details-pop">
                                    <div class="order-detail-mainttl">
                                    </div>
                                    <div class="customer-info-pop">
                                        <div class="customer-name-prnt">
                                        <h2>{{ restaurant.owner }}</h2>
                                        <h3>{{ restaurant.registration_number }}</h3>
                                        </div>
                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-phone" aria-hidden="true"></i>{{ restaurant.contact }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-map-marker" aria-hidden="true"></i>{{ restaurant.street }}, {{ restaurant.town }}, {{ restaurant.state }}- {{ restaurant.zip_code }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-envelope-open-o" aria-hidden="true"></i>{{ restaurant.email }}</span>
                                        </div>

                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-clock-o"></i>Opens at: {{ restaurant.opening_time }} & Closes at: {{ restaurant.closing_time }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-calendar-check-o" aria-hidden="true"></i>Joined at {{ restaurant.joined_date }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-credit-card"></i>Delivery charge: ${{ restaurant.delivery_charge }}</span>
                                        </div>
                                    </div>

                                    <div class="customer-instructions-pop">
                                        <h2>Location</h2>
                                        <div class="fm-ls sm-mb">
                                            <div id="map" style="height: 500px; width: 1100px;"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                    </div>
                </div>
            </div>
            <!-- right body part -->
        </div>
        </div>

    </section>
    {% include 'dashboard/footer.php' %}
    <script>
        $(document).ready(function(){
            if('{{ restaurant.location_point }}' === 'None'){
              var x = 0;
              var y = 0;
              console.log('no location');
            }
            else{
              var y = {{ restaurant.location_point.y }};
              var x = {{ restaurant.location_point.x }};
              console.log('found')
            }

            var points = [y, x];
            var map = L.map('map').setView(points, 19);
            var osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
              maxZoom: 20,
              subdomains:['mt0','mt1','mt2','mt3']
            });
            var googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
              maxZoom: 20,
              subdomains:['mt0','mt1','mt2','mt3']
            });
            var googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
              maxZoom: 20,
              subdomains:['mt0','mt1','mt2','mt3']
            });
            var googleTerrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{
              maxZoom: 20,
              subdomains:['mt0','mt1','mt2','mt3']
            });

            //for changing the layer(layer switcher)
            var baseLayers = {
                "OpenStreetMap": osm,
                "Google Streets": googleStreets,
                "Google Hybrid": googleHybrid,
                "Google Satellite": googleSat,
                "Google Terrain": googleTerrain,
            };

            map.addLayer(googleStreets);
            var layerswitcher = L.control.layers(baseLayers, {}, {collapsed: true}).addTo(map);
            var icons=L.icon({
              iconSize: [44, 45],
              iconAnchor: [10, 22],
              popupAnchor:  [2, -24],
              shadowAnchor: [2, 18],

              iconUrl:"{% static 'images/marker.png' %}",
              shadowUrl: 'https://unpkg.com/leaflet@1.0.3/dist/images/marker-shadow.png'
            });
            var marker = L.marker(points,{icon:icons}).addTo(map);
            marker.bindPopup("<b> {{restaurant.name}} </b>").openPopup();
        });
    </script>

  </body>
</html>
