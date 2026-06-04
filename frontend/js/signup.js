const API_URL = "https://health-guard-caq0.onrender.com";

console.log("Signup button clicked");
async function signup(){

    const fullName =
    document.getElementById(
    "fullName").value;

    const email =
    document.getElementById(
    "email").value;

    const password =
    document.getElementById(
    "password").value;

    const age =
    document.getElementById(
    "age").value;

    const gender =
    document.getElementById(
    "gender").value;

    try{

        const response =
        await fetch(
        `${API_URL}/signup`,
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                full_name:fullName,
                email:email,
                password:password,
                age:parseInt(age),
                gender:gender

            })
        });

        const data =
        await response.json();

        if(data.success){

            localStorage.setItem(
            "token",
            data.token);

            localStorage.setItem(
            "user_id",
            data.user_id);

            localStorage.setItem(
            "user_name",
            fullName);

            document
            .getElementById(
            "message")
            .innerHTML =
            "✅ Account Created";

            setTimeout(()=>{

                window.location.href =
                "dashboard.html";

            },1500);

        }
        else{

            document
            .getElementById(
            "message")
            .innerHTML =
            "❌ Signup Failed";
        }

    }
    catch(error){

        document
        .getElementById(
        "message")
        .innerHTML =
        "❌ Server Error";
    }
}
