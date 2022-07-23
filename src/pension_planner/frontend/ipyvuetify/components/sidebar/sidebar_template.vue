<v-navigation-drawer
    v-model="drawer_open"
    app
    width="30%"
>
    <v-tabs
        v-model="tab"
        grow
        color="white"
        background-color="green darken-1"
    >
      <v-tab id="accounts_tab">
        <v-icon left>
          mdi-account-cash
        </v-icon>
        Konten
      </v-tab>
      <v-tab id="orders_tab">
        <v-icon left>
          mdi-bank-transfer
        </v-icon>
        Aufträge
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
        <v-tab-item>
            <jupyter-widget :widget="tab_item_accounts">
        </v-tab-item>
        <v-tab-item>
            <jupyter-widget :widget="tab_item_orders">
        </v-tab-item>
    </v-tabs-items>
</v-navigation-drawer>