function notyMessage(data) {
    switch (data.status)
    {
        case 200:
            noty({
                text: "<b>" + data.responseJSON.msg + "</b> ",
                layout: "topCenter",
                type: "success",
                timeout: 4000
            });
            break;
        case 500:
            noty({
                text: "<b>" + data.responseJSON.error + "</b> ",
                layout: "topCenter",
                type: "error",
                timeout: 7000
            });
            break;
    }
};

