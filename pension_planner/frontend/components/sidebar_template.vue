<v-navigation-drawer v-model="drawer_open" width="50%">
    <v-toolbar flat>
        <v-toolbar-title>
            Bankkonto #42
        </v-toolbar-title>
    </v-toolbar>
    <v-divider></v-divider>
    <v-menu v-for="menu in menus">
        <template v-slot:activator="{on, attrs }">
            <v-btn x-small :color="menu.color" v-bind="attrs" v-on="on">
                <v-icon>mdi-plus</v-icon> {{menu.text}}
            </v-btn>
        </template>
        <v-list>
            <v-list-item v-for="name in order_types" @click="add_order(menu.side)">
                <v-list-item-title>{{name}}</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</v-navigation-drawer>
