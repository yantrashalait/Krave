{% include 'dashboard/header.php' %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>List of restaurants</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                               <table id="fd-it-ls-dt" class="display">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Owner name</th>
                                            <th>Registration number</th>
                                            <th>Email</th>
                                            <th>Joined date</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in restaurants %}
                                        <tr>
                                            <td>
                                                {{ item.name }}
                                            </td>
                                            <td>{{ item.owner }}</td>
                                            <td>
                                                {{ item.registration_number }}
                                            </td>
                                            <td>
                                                {{ item.email }}
                                            </td>
                                            <td>
                                                {{ item.joined_date }}
                                            </td>
                                            <td class="ac-bt-hl-fd-ls">
                                                <a href="{% url 'dashboard:restaurant-detail' item.id %}" class="btn btn-success">View detail</a>
                                                <a href="{% url 'dashboard:restaurant-payment' item.id %}" class="btn btn-success">Payment info</a>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                    </div>
                </div>
            </div>
            <!-- right body part -->
        </div>
        </div>

    </section>
    {% include 'dashboard/footer.php' %}

  </body>
</html>
