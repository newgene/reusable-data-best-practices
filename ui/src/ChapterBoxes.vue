<template>
  <div class="flex flex-flow-rowwrap intro-chapters">
    <a class="chapter-box-link" v-for="chapter in documentPreviews" 
    :key="chapter.name" :href="chapter.url">
      <div class="chapter-box">
        <p style="font-weight: bold;">{{ chapter.title }}</p>
        <p class="chapter-box-preview">
          {{chapter.preview.substring(0, 100)}}
        </p>
      </div>
    </a>
  </div>
</template>

<script>
export default {
  name: "ChapterBoxes",
  computed: {
    console: () => console,
    window: () => window,
  },
  data: function() {
    let document_previews = JSON.parse(sessionStorage.getItem('document_previews'));
    let entries = JSON.parse(sessionStorage.getItem('toctree_data_json'))[0].entries;

    entries.forEach((entry, i)=>{
      let document_preview = document_previews.find(doc=>doc.document_title==entry.title);
      entries[i].preview = document_preview.preview
      entries[i].url = document_preview.document_url
    })

    return {
      documentPreviews: entries
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