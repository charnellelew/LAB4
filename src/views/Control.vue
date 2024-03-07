<template>
  <v-container>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="text-center">Combination</v-card-title>
          <v-card-subtitle class="text-center mt-2">Enter your four digit passcode</v-card-subtitle>
          <v-card-text class="mt-8 text-center">
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-row>
                <v-col cols="3" v-for="n in 4" :key="n">
                  <v-text-field
                    v-model="passcodeDigits[n-1]"
                    :rules="digitRules"
                    required
                    maxlength="1"
                    single-line
                    dense
                    hide-details
                    @keydown.enter="submitPasscode"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="submitPasscode">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      valid: true,
      passcodeDigits: [],
      digitRules: [(v) => !!v || "Digit is required"],
    };
  },
  computed: {
    passcode() {
      return this.passcodeDigits.join("");
    },
  },
  methods: {
    submitPasscode() {
      if (this.$refs.form.validate()) {
        const passcodeData = { passcode: this.passcode };
        axios
          .post("/api/control", passcodeData)
          .then((response) => {
            console.log(response.data);
            this.$router.push("/success");
          })
          .catch((error) => {
            console.log(error);
            this.$router.push("/error");
          });
      }
    },
  },
  mounted() {
    for (let i = 0; i < 4; i++) {
      this.passcodeDigits.push("");
    }
  },
};
</script>

<style scoped>
.v-card-title, .v-card-subtitle {
  line-height: 1.5;
}
</style>