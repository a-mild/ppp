<div>
    <v-text-field
        id="name"
        v-model="name"
        label="Name"
        color="green darken-1"
        outlined
        @change="update_name"
    >
    </v-text-field>
    <v-select
        v-model="from_acc_id"
        :items="from_acc_id_options"
        label="Von Konto"
        color="green darken-1"
        outlined
        @change="update_from_acc_id"
    >
    </v-select>
    <v-select
        v-model="target_acc_id"
        :items="target_acc_id_options"
        label="Auf Konto"
        color="green darken-1"
        outlined
        @change="update_target_acc_id"
    >
    </v-select>
    <template v-if="date">
        <v-menu
            v-model="date_menu"
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
    </template>
    <template v-if="start_date">
        <v-menu
            v-model="start_date_menu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="290px"
            dark
        >
            <template v-slot:activator="{ on, attrs }">
                <v-text-field
                    v-model="start_date"
                    label="Datum von"
                    prepend-icon="mdi-calendar"
                    readonly
                    outlined
                    color="green darken-1"
                    v-bind="attrs"
                    v-on="on"
                >
            </v-text-field>
            </template>
            <v-date-picker
                v-model="start_date"
                type="month"
                reactive
                dark
                @change="update_start_date"
            >
            </v-date-picker>
        </v-menu>
    </template>
    <template v-if="end_date">
        <v-menu
            v-model="end_date_menu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="290px"
        >
            <template v-slot:activator="{ on, attrs }">
                <v-text-field
                    v-model="end_date"
                    label="Datum bis"
                    prepend-icon="mdi-calendar"
                    readonly
                    outlined
                    color="green darken-1"
                    v-bind="attrs"
                    v-on="on"
                >
            </v-text-field>
            </template>
            <v-date-picker
                v-model="end_date"
                type="month"
                reactive
                dark
                @change="update_end_date"
            >
            </v-date-picker>
        </v-menu>
    </template>
    <v-text-field
        v-model="amount"
        type="number"
        label="Betrag"
        prepend-icon="mdi-cash"
        color="green darken-1"
        outlined
        @change="update_amount"
    >
    </v-text-field>
</div>