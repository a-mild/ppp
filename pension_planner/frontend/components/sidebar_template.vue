<v-navigation-drawer app v-model="drawer_open" width="50%">
    <v-tabs vertical>
      <v-tab>
        <v-icon left>
          mdi-account-cash
        </v-icon>
      </v-tab>
      <v-tab>
        <v-icon left>
          mdi-bank-transfer
        </v-icon>
      </v-tab>
      <v-tab-item>
        <tab-item-accounts></tab-item-accounts>
      </v-tab-item>
      <v-tab-item>
        <tab-item-orders></tab-item-orders>
      </v-tab-item>
    </v-tabs>
</v-navigation-drawer>
