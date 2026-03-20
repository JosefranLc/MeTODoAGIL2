INSERT INTO disciplinas (nome) VALUES 
('Matemática'), 
('Português'), 
('História'), 
('Biologia');

INSERT INTO alunos (nome, matricula, senha_hash) VALUES 
('Arthur BOIBOI', '202300456', '$2y$10$ExampleHashForTest.1234567890');

INSERT INTO notas (aluno_id, disciplina_id, bimestre, valor, descricao) VALUES 
(1, 1, 2, 8.5, 'Prova 1'),
(1, 2, 2, 7.2, 'Prova 1'),
(1, 3, 2, 5.8, 'Trabalho'),
(1, 4, 2, 9.0, 'Prova final');

INSERT INTO frequencias (aluno_id, disciplina_id, data_aula, presente) VALUES 
(1, 1, '2025-08-01', 1),
(1, 1, '2025-08-02', 1),
(1, 3, '2025-08-01', 0);