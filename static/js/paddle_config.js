function getCsrfToken() {
    const name = 'csrftoken';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

window.initiatePurchase = async function(credit_id, token, email, env) {
    try {
        console.log("Initiating purchase for credit:", credit_id, "with token:", token);
        const response = await fetch(`/payment/pay/${credit_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ credit_id: credit_id })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Transaction data:", data);
        
        if (!data.tnx_id) {
            throw new Error("No transaction ID returned from server");
        }
        
        Paddle.Environment.set(env.trim());
        Paddle.Setup({ token: token });
        
        console.log("Opening Paddle checkout with transaction ID:", data.tnx_id);
        Paddle.Checkout.open({
            transactionId: data.tnx_id,
            settings: {
                displayMode: "overlay",
                
                theme : "dark"
              },
            customer:{
                email : email
            },
            customData:{
                credit_id: credit_id,
                user_email: email
            },
            successCallback: function(data) {
                console.log("Payment successful!", data);
                window.location.href = '/payment/success/';
            },
            closeCallback: function(reason) {
                console.log("Checkout closed. Reason:", reason);
            }
        });
    } catch (error) {
        console.error("Error processing payment:", error);
    }
}