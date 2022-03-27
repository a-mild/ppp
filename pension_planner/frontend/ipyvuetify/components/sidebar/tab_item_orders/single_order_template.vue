<div>
    <v-text-field
        v-model="name"
        id="name"
        label="Name"
        color="green darken-1"
        outlined
        @change="update_name"
    >
    </v-text-field>
    <v-select
        v-model="from_acc_id"
        id="from-acc-select"
        :items="from_acc_id_options"
        label="Von Konto"
        color="green darken-1"
        outlined
        @change="update_from_acc_id"
    >
    </v-select>
    <v-select
        v-model="target_acc_id"
        id="target-acc-select"
        :items="target_acc_id_options"
        label="Auf Konto"
        color="green darken-1"
        outlined
        @change="update_target_acc_id"
    >
    </v-select>
    <v-menu
        v-model="datepicker_menu"
        :close-on-content-click="false"
        transition="scale-transition"
        color="green darken-1"
        offset-y
        min-width="290px"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-text-field
                id="date"
                v-model="date"
                label="Datum"
                prepend-icon="mdi-calendar"
                color="green darken-1"
                outlined
                readonly
                v-bind="attrs"
                v-on="on"
            >
        </v-text-field>
        </template>
        <v-date-picker
            v-model="date"
            type="month"
            reactive
            dark
            @change="update_date"
        >
        </v-date-picker>
    </v-menu>
    <v-text-field
        v-model="amount"
        id="amount"
        type="number"
        label="Betrag"
        color="green darken-1"
        prepend-icon="mdi-cash"
        outlined
        @change="update_amount"
    >
    </v-text-field>
</div>