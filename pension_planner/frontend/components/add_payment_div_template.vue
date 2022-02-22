<template>
    <v-menu v-model="menu" offset-y>
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                icon
                v-bind="attrs"
                v-on="on"
            >
                <v-icon>mdi-plus-box</v-icon>
            </v-btn>
        </template>
        <v-list>
            <v-list-item v-for="name in payment_names" @click="add_payment(name)">
                <v-list-item-title>{{ name }}</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</template>