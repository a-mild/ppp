<v-container>
    <v-row>
    <v-tabs-items v-model="tab" id="tabs-items-orders">
        <v-tab-item v-for="(order, id_) in orders" >
            <jupyter-widget :widget="order.widget" />
        </v-tab-item>
    </v-tabs-items>
    </v-row>
    <v-row>
        <v-tabs v-model="tab" vertical id="tabs-orders">
            <v-tab v-for="(order, id_) in orders" style="text-transform: none !important;">
                {{ order.name }}
                <v-btn icon @click.stop="delete_order(id_)">
                    <v-icon>mdi-trash-can</v-icon>
                </v-btn>
            </v-tab>
        </v-tabs>
    </v-row>
    {{output}}
</v-container>