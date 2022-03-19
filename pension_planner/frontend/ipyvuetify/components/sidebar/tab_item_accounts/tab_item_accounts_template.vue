<div id="tab-item_accounts">
    <v-btn id="open_account" @click="open_account">
        <v-icon>mdi-plus-box</v-icon>
        Account eröffnen
    </v-btn>
    <v-divider></v-divider>
    <v-container>
        <v-row>
            <v-tabs-items v-model="tab">
                <v-tab-item v-for="(acc, id_) in accounts">
                    <v-text-field
                        label="Kontoname"
                        v-model="acc.name"
                        @input="update_name(acc)"
                    >
                    </v-text-field>
                    <v-text-field
                        type="number"
                        label="Zinsen [% p.a.]"
                        v-model="acc.interest_rate"
                        @input="update_interest_rate(acc)"
                    >
                    </v-text-field>
                </v-tab-item>
            </v-tabs-items>
        </v-row>
        </v-container>
        <v-row>
            <v-tabs v-model="tab" vertical>
                <v-tab v-for="(acc, id) in accounts" style="text-transform: none !important;">
                    {{ acc.name }}
                </v-tab>
            </v-tabs>
        </v-row>
    <v-container>
    {{ output }}
</div>
