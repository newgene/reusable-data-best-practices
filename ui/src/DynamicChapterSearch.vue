<template>
  <div id="search">
    <div id="search-header-wrapper">
      <input class="dynamic-search-input" placeholder="Search chapters" v-model="query"
      v-on:keyup.enter="submit" @keyup="doSomething"/>
      <div v-if="this.query !== ''">
        <p><b>{{ this.matchCount }}</b> matches found in <b>{{ this.chapterMatchCount }}</b> 
        {{ this.chapterMatchCount==1?'chapter': 'chapters' }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DynamicChapterSearch",
  computed: {
    console: () => console,
    window: () => window,
  },
  data: function() {
    let document_previews_value = sessionStorage.getItem('document_previews');
    let search_svg_path = sessionStorage.getItem('search_svg_path');
    let search_path = sessionStorage.getItem('search_path');

    return {
        query: '',
        queryMatches: [],
        matchCount: 0,
        chapterMatchCount: 0,
        documentPreviews: JSON.parse(document_previews_value),
        searchSvgPath: search_svg_path,
        searchPath: search_path,
    };
  },
  privateState:{
    matchCount:0,
    searchBubbleShown:false,
  },
  methods: {
    doSomething: function () {
      // reset values
      this.queryMatches.length = 0;
      let queryMatches = []
      this.matchCount = 0;
      this.chapterMatchCount = 0;

      // start searching for results
      this.documentPreviews.forEach(doc_preview => {
        let count = doc_preview.preview.toLowerCase().split(this.query).length - 1;
        count = count + doc_preview.document_title.toLowerCase().split(this.query).length - 1
        let searchUrl = window.location.pathname.includes('/chapters/') ?
            doc_preview.document_url.replace('chapters/', '') + '?highlight=' + this.query :
            doc_preview.document_url + '?highlight=' + this.query
        queryMatches.push({
          documentName: doc_preview.document_name, count: count,
          documentTitle: doc_preview.document_title, documentUrl: doc_preview.document_url,
          searchUrl: searchUrl
        })
      })

      queryMatches.forEach(match=>{
        try{
          let chapterBoxElement = document.getElementById(match.documentUrl);
          // there is an initial flash with the count when the query is "" which basically counts
          // all the characters in the documents
          // this is not really needed, just prevents the flashing
          if(this.query!==""){
            this.matchCount += match.count;
          }

          if(chapterBoxElement){
            if(match.count===0){
              chapterBoxElement.style.opacity = 0.3;
            }else{
              chapterBoxElement.style.opacity = 1;
              this.chapterMatchCount = this.chapterMatchCount + 1;
            }
          }
          
        }catch(e){
          console.error(e);
        }
      })
    },
    submit: function () {
      if (this.query) {
        window.location.href = this.searchPath + "?q=" + this.query
      }
    }
  }
}
</script>

<style scoped>
.dynamic-search-input{
  background-position: 8px 6px !important;
  border: 0;
  height: 32px;
  border-bottom: 2px solid #3e99af;
  padding: 5px 15px;
  font-size: 1.6rem;
  margin: 25px;
  outline: none;
  transition: all 0.1s;
}

.dynamic-search-input:focus{
  border-bottom: 7px solid #3e99af;
}
</style>