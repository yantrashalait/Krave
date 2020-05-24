{% include 'dashboard/header.php' %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>Restaurant Requests</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                               <table id="fd-it-ls-dt" class="display">
                                    <thead>
                                        <tr>
                                            <th>Date</th>
                                            <th>Name of restaurant</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in req %}
                                        <tr>
                                            <td>{{ item.requested_date }}</td>
                                            <td>
                                                {{ item.name }}
                                            </td>
                                            <td>
                                                <a href="{% url 'dashboard:request-detail' item.pk %}" class="btn btn-success">View Detail</a>
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
