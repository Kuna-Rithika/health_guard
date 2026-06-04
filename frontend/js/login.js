const API_URL = "https://health-guard-caq0.onrender.com";

async function login(){

    const email =
    document.getElementById(
    "email").value;

    const password =
    document.getElementById(
    "password").value;

    try{

        const response =
        await fetch(
        `${API_URL}/login`,
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                email:email,
                password:password

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
            data.user.id);

            localStorage.setItem(
            "user_name",
            data.user.name);

            document
            .getElementById(
            "message")
            .innerHTML =
            "✅ Login Successful";

            setTimeout(()=>{

                window.location.href =
                "dashboard.html";

            },1000);

        }
        else{

            document
            .getElementById(
            "message")
            .innerHTML =
            "❌ Invalid Login";
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