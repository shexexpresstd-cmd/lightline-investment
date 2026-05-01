$routes = @("/", "/engineering/", "/logistics/", "/capital/", "/research/", "/cfe/")
foreach ($u in $routes) {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:5000$u" -UseBasicParsing
    Write-Host "$u -> $($r.StatusCode)"
}
