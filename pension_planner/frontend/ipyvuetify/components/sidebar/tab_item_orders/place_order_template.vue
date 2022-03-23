<template>
    <v-row>
        <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  small
                  dark
                  v-bind="attrs"
                  v-on="on"
                  id="place_order_btn"
                >
                    <v-icon>mdi-plus</v-icon>
                    Neuer Auftrag
                </v-btn>
            </template>
            <v-list id="order_option_list">
                <v-list-item
                  v-for="name in order_names"
                  :id=name
                  @click="place_order(name)"
                >
                  <v-list-item-title>{{ name }}</v-list-item-title>
                </v-list-item>
              </v-list>
        </v-menu>
    </v-row>
</template>