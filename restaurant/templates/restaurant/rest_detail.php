{% include 'restaurant/header.php' %}
{% load static %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>Edit Your Restaurant Details</h1>
                                </div>
                                <!-- <div class="ac-bt-hl">
                                      <button class="ac-bt">Save</button>
                                    </div> -->
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <form method="POST" action="." enctype="multipart/form-data">
                                    {% csrf_token %}
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Name</label>
                                        {{ form.name }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td">
                                            <div class="up-im">
                                                <input type='file' name="logo" id="id_logo" />
                                                <div class="up-im-bt">
                                                    <div class="up-im-cn">
                                                        <div class="up-im-bt-tl">
                                                            <p>Drop image here to upload</p>
                                                        </div>
                                                        <div class="up-im-bt-dv">
                                                            <p>or</p>
                                                        </div>
                                                        <div class="up-im-bt-bw">
                                                            Browse File
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="pv-im-hl">
                                            {% if request.restaurant.logo %}
                                                <img id="blah" src="{{ request.restaurant.logo.url }}" alt="your image" />
                                            
                                            {% else %}
                                                <img id="blah" src="{% static 'restaurant/images/rest_logo.jpg' %}" alt="your image" />
                                            {% endif  %}

                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Street</label>
                                        {{ form.street }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Town</label>
                                        {{ form.town }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>State</label>
                                        {{ form.state }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Zip Code</label>
                                        {{ form.zip_code }}
                                    </div>
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Contact Number</label>
                                        {{ form.contact }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Email Address</label>
                                        {{ form.email }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Registration Number</label>
                                        {{ form.registration_number }}
                                    </div>
                                    <!-- form list -->                                    
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Opening Time</label>
                                                {{ form.opening_time }}
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Closing TIme</label>
                                                {{ form.closing_time }}
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Delivery Time</label>
                                                {{ form.delivery_time }}
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Delivery Charge</label>
                                                {{ form.delivery_charge }}
                                            </div>
                                        </div>
                                    </div>   
                                    {% if rest_cuisine %} 
                                    <div class="fm-ls sm-mb">
                                        <label>Selected Cuisines</label>
                                        <p>
                                        {% for item in rest_cuisine.cuisine.all %}
                                            {{ item.name }}
                                        {% endfor %}
                                        </p>
                                        
                                    </div>
                                    {% endif %}
                                    <!-- form list -->                               
                                    <div class="fm-ls sm-mb">
                                        <label>Types of Cuisines</label>
                                        
                                            <select name="cuisines[]" class="fd-ct" multiple="multiple">
                                                <option></option>
                                                {% for item in cuisine %}
                                                <option value="{{ item.id }}">{{ item.name }}</option>
                                                {% endfor %}
                                            </select>
                                              
                                    </div>
                                    {{ form.media }}
                                    <div class="fm-ls sm-mb">
                                        <div id="map" style="height: 1000px; width: 1000px;"></div>
                                    </div>
                                    <input type="text" id="lat" name="lat" hidden value="{{ request.restaurant.latitude }}" />
                                    <input type="text" id="lon" name="lon" hidden value="{{ request.restaurant.longitude }}" />
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                      <button type="submit" class="sb-bt mx-auto d-flex">Update Restaurant Details</button>
                                    </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <!-- right body part -->
        </div>
        </div>

    </section>
    
    {% include 'restaurant/footer.php' %}
    <script>
        if ('{{ request.restaurant.location_point }}' != ''){
            var points = [{{ request.restaurant.latitude }}, {{ request.restaurant.longitude }}];
        }
        else{
            var points = [40.730610, -73.935242];
        }
        map = L.map('map', {doubleClickZoom: false}).locate({setView: true, maxZoom: 16});

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


        map.on('click',function(e){
            lat = e.latlng.lat;
            lon = e.latlng.lng;

            //Clear existing marker, 
            if (marker != undefined) {
                map.removeLayer(marker);
                console.log(lat);
                console.log('clicked')
                $('#lat').val(lat);
                $("#lon").val(lon);
            };

            //Add a marker to show where you clicked.
            marker = L.marker([lat,lon], {icon:icons}).addTo(map);  
        });
    </script>

  </body>
</html>