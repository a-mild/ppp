<template>
    <v-row>
        <v-col>
            <v-menu offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      id="place_order_btn"
                      color="green darken-1"
                      small
                      dark
                      v-bind="attrs"
                      v-on="on"
                    >
                        <v-icon>mdi-plus</v-icon>
                        Neuer Auftrag
                    </v-btn>
                </template>
                <v-list id="order_option_list">
                    <v-list-item
                      :id=name
                      v-for="name in order_names"
                      @click="place_order(name)"
                    >
                      <v-list-item-title>{{ name }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
            </v-menu>
        </v-col>
    </v-row>
</template>