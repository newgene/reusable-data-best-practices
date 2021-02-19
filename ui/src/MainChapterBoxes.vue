<template>
  <div class="flex chapters-container featured-container">
    <h1 style="font-weight: bold; color: white; margin-top: 0;">Featured</h1>
    <div class="flex flex-flow-rowwrap intro-chapters">
      <a class="chapter-box-link" v-for="chapter in documentPreviews.slice(0,3)" 
      :key="chapter.document_name" :href="chapter.document_url">
        <div class="chapter-box" style="background-color: #212121 !important; color: white;">
          <p style="font-weight: bold;">{{ chapter.document_title }}</p>
          <p class="chapter-box-preview">
            {{chapter.preview.substring(0, 100)}}
          </p>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainChapterBoxes",
  computed: {
    console: () => console,
    window: () => window,
  },
  data: function() {
    let document_previews = sessionStorage.getItem('document_previews');

    return {
      documentPreviews: JSON.parse(document_previews)
    }
  }
}
</script>

<style scoped>
.chapter-box-link{
  text-decoration: none !important;
}
.chapter-box{
  margin: 10px;
  cursor: pointer;
  box-shadow: 0 4.5px 5.6px rgb(0 0 0 / 3%), 0 15px 18.8px rgb(0 0 0 / 4%), 0 67px 84px rgb(0 0 0 / 7%);
  background-color: white;
  border: 5px solid transparent;
  box-sizing: border-box;
  min-height: 200px;
  height: auto;
  width: 240px;
  border-radius: 10px;
  padding: 20px;
  -webkit-transition: all 0.2s ease;
  -moz-transition: all 0.2s ease;
  -ms-transition: all 0.2s ease;
  -o-transition: all 0.2s ease;
  transition: all 0.2s ease;
}
.chapter-box-preview{
    color: #a5a5a5;
    font-size: 0.8em;
}
</style>