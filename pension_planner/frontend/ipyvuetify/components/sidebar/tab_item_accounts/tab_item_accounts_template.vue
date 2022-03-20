<div id="tab-item-accounts">
    <v-btn id="open_account" @click="open_account">
        <v-icon>mdi-plus-box</v-icon>
        Account eröffnen
    </v-btn>
    <v-divider></v-divider>
    <v-container>
        <v-row>
            <v-tabs v-model="tab" vertical id="tabs-accounts">
                <v-tab v-for="(acc, id) in accounts" style="text-transform: none !important;">
                    {{ acc.name }}
                </v-tab>
            </v-tabs>
        </v-row>
        <v-row justify="center">
            <v-tabs-items v-model="tab" id="tabs-items-accounts">
                <v-tab-item v-for="(acc, id_) in accounts" >
                    <v-text-field
                        label="Kontoname"
                        v-model="acc.name"
                        @input="update_name(id_)"
                        id="account_name"
                        outlined
                    >
                    </v-text-field>
                    <v-text-field
                        type="number"
                        label="Zinsen [% p.a.]"
                        v-model="acc.interest_rate"
                        @input="update_interest_rate(id_)"
                        id="interest_rate"
                        outlined
                    >
                    </v-text-field>
                </v-tab-item>
            </v-tabs-items>
        </v-row>
    </v-container>
    {{ output }}
</div>
