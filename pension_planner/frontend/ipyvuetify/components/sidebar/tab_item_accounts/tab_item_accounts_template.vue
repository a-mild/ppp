<v-container
    id="tab-item-accounts"
    fluid
>
    <v-row>
        <v-col>
            <v-btn
                id="open_account"
                color="green darken-1"
                dark
                small
                @click="open_account"
            >
                <v-icon>mdi-plus-box</v-icon>
                Neues Konto eröffnen
            </v-btn>
        </v-col>
    </v-row>
    <v-row>
        <v-col>
            <v-tabs-items v-model="tab" id="tabs-items-accounts">
                <v-tab-item v-for="(acc, id_) in accounts" >
                    <v-text-field
                        v-model="acc.name"
                        id="account_name"
                        label="Kontoname"
                        color="green darken-1"
                        outlined
                        @change="update_name(id_)"
                    >
                    </v-text-field>
                    <v-text-field
                        v-model="acc.interest_rate"
                        id="interest_rate"
                        type="number"
                        label="Zinsen [% p.a.]"
                        color="green darken-1"
                        outlined
                        @change="update_interest_rate(id_)"
                    >
                    </v-text-field>
                </v-tab-item>
            </v-tabs-items>
        </v-col>
    </v-row>
    <v-row>
        <v-col>
            <v-tabs
                v-model="tab"
                id="tabs-accounts"
                color="green darken-1"
                vertical
            >
                <v-tab v-for="(acc, id_) in accounts" style="text-transform: none !important;">
                    {{ acc.name }}
                    <v-btn icon @click.stop="delete_account(id_)">
                        <v-icon>mdi-trash-can</v-icon>
                    </v-btn>
                </v-tab>
            </v-tabs>
        </v-col>
    </v-row>
</v-container>
