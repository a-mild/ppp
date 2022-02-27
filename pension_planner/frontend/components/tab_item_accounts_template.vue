<div>
    <v-btn @click="open_account">
        <v-icon>mdi-circle-plus</v-icon>
        Account eröffnen
    </v-btn>
    <v-divider></v-divider>
    <v-text-field
        label="Kontoname"
        v-model="account_name"
    >
    </v-text-field>
    <v-text-field
        type="number"
        label="Zinsen [% p.a.]"
        v-model="interest_rate"
    >
    </v-text-field>
</div>
