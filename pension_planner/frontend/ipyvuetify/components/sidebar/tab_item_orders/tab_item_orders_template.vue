<div id="tab-item-orders">
    <v-container>
            <jupyter-widget :widget="place_order" />
        <v-row>
            <jupyter-widget :widget="order_editor" id="order_editor"/>
        </v-row>
        <!--
        <v-row>
            <jupyter-widget :widget="overview" />
        </v-row>
        -->
    </v-container>
</div>