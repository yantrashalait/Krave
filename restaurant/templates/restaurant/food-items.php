{% include 'restaurant/header.php' %}
{% load static %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>Items</h1>
                                </div>
                                <!-- <div class="ac-bt-hl">
                                      <button class="ac-bt">Save</button>
                                    </div> -->
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <table id="fd-it-ls-dt" class="display">
                                    <thead>
                                        <tr>
                                            <th>Display Name</th>
                                            <th>Price</th>
                                            <th>Category</th>
                                            <th>Edit/Delete</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Chicken Sandwich</td>
                                            <td>$5.00</td>
                                            <td><a href="categories-detail.php">Sandwiches</a></td>
                                            <td class="ac-bt-hl-fd-ls">
                                                <a class="btn btn-primary" href="#"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a>
                                                <a class="btn btn-danger" href="#"><i class="fa fa-trash-o" aria-hidden="true"></i></a>
                                            </td>
                                        </tr>
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
    {% include 'restaurant/footer.php' %}