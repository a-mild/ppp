<template>
    <div id="place_order_buttons">
        <v-btn v-for="name in order_names" x-small @click=place_order(name) :id=name>
            <v-icon>mdi-plus-box</v-icon>
            {{name}}
        </v-btn>
    </div>
</template>