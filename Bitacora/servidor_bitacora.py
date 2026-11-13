elif url.path == "/incidencias":
            lista = incidencias
            # Filtrar por tipo si está presente en los parámetros de consulta
            if "tipo" in parametros:
                lista = [i for i in lista if i["tipo"] == parametros["tipo"][0]]
            # Filtrar por estado si está presente en los parámetros de consulta
            if "estado" in parametros:
                lista = [i for i in lista if i["estado"] == parametros["estado"][0]]
            self._enviar(200, lista)