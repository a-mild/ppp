<v-navigation-drawer app v-model="drawer_open" width="25%">
    <v-tabs-items v-model="tabs">
      <v-tab-item
        v-for="item in tabs"
      >
        <v-card flat>
          <v-card-text>{{ item }}</v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
    <jupyter-widget :widget="parts.add" />
    <v-divider></v-divider>
    <jupyter-widget :widget="parts.editor" />
</v-navigation-drawer>
