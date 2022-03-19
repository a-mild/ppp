<v-navigation-drawer app v-model="drawer_open" width="50%">
    <v-tabs grow>
      <v-tab>
        <v-icon left>
          mdi-account-cash
        </v-icon>
        Accounts
      </v-tab>
      <v-tab>
        <v-icon left>
          mdi-bank-transfer
        </v-icon>
        Aufträge
      </v-tab>
          <v-tab-item>
            <jupyter-widget :widget="tab_item_accounts">
          </v-tab-item>
          <!--
          <v-tab-item>
            <jupyter-widget :widget="tab_item_orders">
          </v-tab-item>
          -->
    </v-tabs>
</v-navigation-drawer>
