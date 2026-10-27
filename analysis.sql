.headers on
.mode column

SELECT '== Top components per model ==';
SELECT c.model, cc.component, COUNT(*) AS n
FROM complaint_components cc
JOIN complaints c ON c.odi_number = cc.odi_number
GROUP BY c.model, cc.component
HAVING n >= 20
ORDER BY c.model, n DESC;

SELECT '== Crash, fire, injuries by model ==';
SELECT model, COUNT(*) AS complaints,
       ROUND(AVG(crash) * 100, 1) AS crash_pct,
       ROUND(AVG(fire) * 100, 1) AS fire_pct,
       SUM(injuries) AS injuries, SUM(deaths) AS deaths
FROM complaints
GROUP BY model
ORDER BY crash_pct DESC;

SELECT '== RAV4 fire complaints by component ==';
SELECT cc.component, COUNT(*) AS n
FROM complaints c
JOIN complaint_components cc ON c.odi_number = cc.odi_number
WHERE c.model = 'rav4' AND c.fire = 1
GROUP BY cc.component
ORDER BY n DESC;

SELECT '== Complaints by filed year ==';
SELECT substr(filed_date, 1, 4) AS year,
       SUM(model = 'cr-v') AS crv, SUM(model = 'camry') AS camry,
       SUM(model = 'civic') AS civic, SUM(model = 'rav4') AS rav4,
       SUM(model = 'corolla') AS corolla, COUNT(*) AS total
FROM complaints
GROUP BY year
ORDER BY year;
