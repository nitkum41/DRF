const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')

const contentContainer = document.getElementById('content-container')
const baseEndPoint = 'http://localhost:8000/api'


if(loginForm){
    //handle login
    loginForm.addEventListener('submit',handleLogin)
}

if(searchForm){
    //handle search
    searchForm.addEventListener('submit',handleSearch)
}

function handleLogin(event){
    event.preventDefault()

    const loginEndPoint =`${baseEndPoint}/token/`
    
    let loginFormData = new FormData(loginForm) //read data from the form
    let loginObjectData = Object.fromEntries(loginFormData) //convrt into object

    let bodyStr = JSON.stringify(loginObjectData)  //convert object into string
    
    const options = {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:bodyStr
    }

    // console.log('call fetch',loginEndPoint)

    fetch(loginEndPoint,options).then(response=>{
        console.log(response)
        return response.json()
    }).then(authData=>{handleAuthData(authData,getProductList)
    }).catch(err=>{
        console.log("Error in side promise:",err)
    })
}


function handleSearch(event){
    event.preventDefault()

    let formData = new FormData(searchForm)
    let data = Object.fromEntries(formData)
    let searchParams = new URLSearchParams(data) //read search parameter from url

    const endpoint =`${baseEndPoint}/search?${searchParams}`
    const headers = {
        "Content-Type":"application/json"
    }
    const authToken = localStorage.getItem('access') //read token from memory
    if(authToken){
        headers["Authorization"]=`Bearer ${authToken}`
    }
    const options = {
        method:"GET",
        headers: headers,
    }

    // console.log('call fetch',loginEndPoint)

    fetch(endpoint,options).then(response=>{
        console.log(response)
        return response.json()
    })
    .then(data=>{
        // console.log(data.hits)
        //check for invalid token
        const validData = isTokenNotValid(data)
        if (validData && contentContainer){
            contentContainer.innerHTML=""

            if(data && data.hits){
                let htmlStr = ""

                for (let result of data.hits){
                    htmlStr+="<li>"+ result.title + "</li>"
                }

                contentContainer.innerHTML = htmlStr
                if(data.hits.length === 0){

                    contentContainer.innerHTML = "<p> No Result Found </p>"
                }
            }
            else{
                contentContainer.innerHTML = "<p> No Result Found </p>"
            }
        }

        // writeToContainer(data)
    })
    .catch(err=>{
        console.log("Error in side promise:",err)
    })

}


function handleAuthData(authdata,callback){
    localStorage.setItem('access',authdata.access)
    localStorage.setItem('refresh',authdata.refresh)
    if (callback){
        callback()
    }
}


function writeToContainer(data){
    if (contentContainer){
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data,null,4)+"</pre>"
    }
}

function getFetchOptions(method,body){
     return  {
        method:method===null ? "GET": method,
        headers:{
            "Content-Type":"application/json",
            "Authorization":`Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
}

function isTokenNotValid(jsonData){
    if(jsonData.code && jsonData.code === "token_not_valid"){

        alert("please login again")
        return false
    }
    return true
}

function validateJWTToken(){
    //fetch
    const endpoint =`${baseEndPoint}/token/verify/`
    const options = {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            token:localStorage.getItem('access')
        })
    }

    fetch(endpoint,options)
    .then(response=> {
        return response.json()
    })
    .then(x=>{
        //refresh token
        console.log(x)
        // isTokenNotValid(x)
    })



}




function getProductList(){
    const endpoint =`${baseEndPoint}/products/`
    const options = getFetchOptions()
    
    fetch(endpoint,options)
    .then(response=>{
        return response.json()})
    .then(data=>{

        const validData= isTokenNotValid(data)
        if (validData){
            writeToContainer(data)
        }
        
    })

}

// const searchClient = algoliasearch(appID,'key')
const searchClient = algoliasearch('PFZUMEWIAA', 'e78bdc757e0ee7c9ddcd6855345cba7f');

const search = instantsearch({
  indexName: 'cfe_Product',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),

  //clear refinements
  instantsearch.widgets.clearRefinements({
    container: '#clear-refinements'
}),

//refinement based on indexing declared in products
  instantsearch.widgets.refinementList({
      container: '#user-list',
      attribute: 'user'
  }),

  instantsearch.widgets.refinementList({
    container: '#public-list',
    attribute: 'public'
}),

//add highlighter in the results
  instantsearch.widgets.hits({
    container: '#hits',
    templates:{
        item: `<div> 
          <div>  {{#helpers.highlight}}{"attribute":"title"}{{/helpers.highlight}}</div> 
          <div>  {{#helpers.highlight}}{"attribute":"body"}{{/helpers.highlight}} </div>

          
           <p> {{user}} </p> 
           <p>\${{ price }}</p>
        
        </div>`
    }
    })
    
  
]);

search.start();

// validateJWTToken()
// getProductList()