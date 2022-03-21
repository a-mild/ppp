<v-container id="tab-item-accounts">
    <v-row>
    <v-btn id="open_account" @click="open_account">
        <v-icon>mdi-plus-box</v-icon>
        Konto eröffnen
    </v-btn>
    </v-row>
    <v-row>
        <v-tabs-items v-model="tab" id="tabs-items-accounts">
            <v-tab-item v-for="(acc, id_) in accounts" >
                <v-text-field
                    label="Kontoname"
                    v-model="acc.name"
                    @change="update_name(id_)"
                    id="account_name"
                    outlined
                >
                </v-text-field>
                <v-text-field
                    type="number"
                    label="Zinsen [% p.a.]"
                    v-model="acc.interest_rate"
                    @change="update_interest_rate(id_)"
                    id="interest_rate"
                    outlined
                >
                </v-text-field>
            </v-tab-item>
        </v-tabs-items>
    </v-row>
    <v-row>
        <v-tabs v-model="tab" vertical id="tabs-accounts">
            <v-tab v-for="(acc, id_) in accounts" style="text-transform: none !important;">
                {{ acc.name }}
                <v-btn icon @click.stop="delete_account(id_)">
                    <v-icon>mdi-trash-can</v-icon>
                </v-btn>
            </v-tab>
        </v-tabs>
    </v-row>
    {{ output }}
</v-container>
