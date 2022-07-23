<div>
<v-expansion-panels accordion>
    <jupyter-widget v-for="acc in accounts" :widget="acc" />
</v-expansion-panels>
{{output}}
</div>
