{% include 'dashboard/header.php' %}
{% load static %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>{{ staff.username|title }}</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <div class="order-details-pop">
                                    <div class="order-detail-mainttl">
                                    </div>
                                    <div class="customer-info-pop">
                                        <div class="customer-name-prnt">
                                          <h2>{{ staff.first_name|title }} {{ staff.last_name|title }}</h2>
                                          <h3>Last login: {{ staff.last_login }}</h3>
                                        </div>
                                        <div class="pv-im-hl">
                                            <img src="{{ staff.profile.image.url }}">
                                        </div>
                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-phone" aria-hidden="true"></i>{{ staff.profile.contact }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-map-marker" aria-hidden="true"></i>{{ staff.profile.address }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-envelope-open-o" aria-hidden="true"></i>{{ staff.email }}</span>
                                        </div>

                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-calendar-check-o" aria-hidden="true"></i>Joined at {{ staff.date_joined }}</span>
                                        </div>

                                        <div class="customer-instructions-pop">
                                            <h2>Last Location</h2>
                                            <div class="fm-ls sm-mb">
                                                <div id="map" style="height: 500px; width: 1100px;"></div>
                                            </div>
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
            if('{{ staff.location }}' === ''){
              var x = 0;
              var y = 0;
              console.log('no location');
            }
            else{
              var y = {{ staff.location.last_location_point.y }};
              var x = {{ staff.location.last_location_point.x }};
              console.log('found')

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
              marker.bindPopup("<b> {{staff.location.tracked_date}} </b>").openPopup();
          }
        });
    </script>
  </body>
</html>
