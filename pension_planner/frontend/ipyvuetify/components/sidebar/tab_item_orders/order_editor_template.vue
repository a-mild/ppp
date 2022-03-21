<v-container>
    <v-tabs-items v-model="tab" >
        <v-tab-item v-for="(order, id_) in orders" >
            <jupyter-widget :widget="order" />
        </v-tab-item>
    </v-tabs-items>
    {{output}}
</v-container>