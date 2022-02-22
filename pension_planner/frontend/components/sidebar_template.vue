<v-navigation-drawer app v-model="drawer_open" width="50%">
    <v-toolbar flat>
        <v-toolbar-title>
            Bankkonto #42
        </v-toolbar-title>
    </v-toolbar>
    <v-divider></v-divider>
    <v-menu v-model="menu" offset-y>
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                color="black"
                v-bind="attrs"
                v-on="on"
            >
                <v-icon>mdi-plus</v-icon>Neue Einzahlung
            </v-btn>
        </template>
        <v-list>
            <v-list-item v-for="name in order_types">
                <v-list-item-title>{{name}}</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</v-navigation-drawer>
