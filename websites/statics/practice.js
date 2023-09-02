
async function get_data(){
    const response  = await fetch('/api');
    const data = response.json();
    console.log(data);
}
get_data();