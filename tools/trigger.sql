CREATE FUNCTION update_annotations_approved_by_id_function()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE examples_example
  SET annotations_approved_by_id = NEW.confirmed_by_id
  WHERE id = NEW.example_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION update_annotations_approved_by_role_id_function()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE examples_example
  SET annotations_approved_by_role_id = (SELECT role_id FROM projects_member WHERE project_id = (SELECT project_id FROM examples_example WHERE id = NEW.example_id) AND user_id = NEW.confirmed_by_id)
  WHERE id = NEW.example_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION reset_annotations_approved_by_id_function()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE examples_example
  SET annotations_approved_by_id = NULL
  WHERE id = OLD.example_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION reset_annotations_approved_by_role_id_function()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE examples_example
  SET annotations_approved_by_role_id = NULL
  WHERE id = OLD.example_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER reset_annotations_approved_by_id
AFTER DELETE ON examples_examplestate
FOR EACH ROW
EXECUTE FUNCTION reset_annotations_approved_by_id_function();

CREATE TRIGGER update_annotations_approved_by_id
AFTER INSERT ON examples_examplestate
FOR EACH ROW
EXECUTE FUNCTION update_annotations_approved_by_id_function();

CREATE TRIGGER reset_annotations_approved_by_role_id
AFTER DELETE ON examples_examplestate
FOR EACH ROW
EXECUTE FUNCTION reset_annotations_approved_by_role_id_function();

CREATE TRIGGER update_annotations_approved_by_role_id
AFTER INSERT ON examples_examplestate
FOR EACH ROW
EXECUTE FUNCTION update_annotations_approved_by_role_id_function();